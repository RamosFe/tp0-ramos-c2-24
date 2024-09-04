package common

import (
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/protocol"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/utils"
	"github.com/op/go-logging"
	"net"
	"os"
	"strconv"
	"time"
)

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID             string
	ServerAddress  string
	LoopAmount     int
	LoopPeriod     time.Duration
	CsvFilename    string
	BatchMaxAmount int
}

type Client struct {
	config  ClientConfig
	batcher protocol.Batcher
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	return &Client{config: config, batcher: *protocol.NewBatcher(config.BatchMaxAmount)}
}

func (c *Client) LogError(action string, err error) {
	log.Criticalf(
		"action: %s | result: fail | client_id: %v | error: %v",
		action,
		c.config.ID,
		err,
	)
}

func (c *Client) SendBatch(conn *net.Conn) error {
	response, err := protocol.SendBets(conn, c.batcher.ToBytes())
	if err != nil {
		c.LogError("send_bet", err)
		return err
	}

	if response.FlagType == protocol.FlagTypeOK {
		log.Infof("action: send_bet | result: success | client_id: %v | number_of_bets: %v",
			c.config.ID,
			c.batcher.Counter,
		)
	} else if response.FlagType == protocol.FlagTypeERROR {
		log.Infof("action: send_bet | result: failed | client_id: %v | msg: failed from server side",
			c.config.ID,
		)
	} else {
		log.Infof("action: send_bet | result: failed | client_id: %v | msg: unexpected response flag %v",
			c.config.ID,
			response.FlagType,
		)
	}

	c.batcher.Reset()
	return nil
}

// StartClientLoop Gets the bet from the envs and send it to the server
func (c *Client) StartClientLoop(terminateChan chan os.Signal) {
	conn, err := net.Dial("tcp", c.config.ServerAddress)
	if err != nil {
		c.LogError("connect", err)
		return
	}
	defer conn.Close()

	agency, err := strconv.Atoi(c.config.ID)
	if err != nil {
		c.LogError("create_bet", err)
		return
	}

	bets, err := utils.ReadBetCSV(c.config.CsvFilename, agency)
	if err != nil {
		c.LogError("read_csv", err)
		return
	}

	for _, bet := range bets {
		select {
		case <-terminateChan:
			log.Infof("action: sigterm_signal | result: success | client_id: %v", c.config.ID)
			return
		default:
			payloadBytes := bet.ToBytes()

			// Checks if batcher is full
			if c.batcher.IsFullWithNewItem(payloadBytes) {
				if err := c.SendBatch(&conn); err != nil {
					return
				}
			}

			if err := c.batcher.Add(payloadBytes); err != nil {
				c.LogError("send_bet", err)
				return
			}
		}
	}

	if !c.batcher.IsEmpty() {
		if err := c.SendBatch(&conn); err != nil {
			return
		}
	}

	flag := protocol.ResponseFlag{
		Identifier: protocol.Identifier{Type: protocol.IdentifierTypeFlag},
		FlagType:   protocol.FlagTypeEND,
	}

	if err = utils.WriteToSocket(conn, flag.ToBytes()); err != nil {
		c.LogError("send_end", err)
		return
	}

	log.Infof("action: send_end | result: success | client_id: %v", c.config.ID)
}
