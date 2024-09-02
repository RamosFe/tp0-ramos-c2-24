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

// TODO - Handle configuration error Batcher size
// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	return &Client{config: config, batcher: *protocol.NewBatcher(config.BatchMaxAmount)}
}

// StartClientLoop Gets the bet from the envs and send it to the server
func (c *Client) StartClientLoop(terminateChan chan os.Signal) {
	conn, err := net.Dial("tcp", c.config.ServerAddress)
	if err != nil {
		log.Criticalf(
			"action: connect | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}
	defer conn.Close()

	agency, err := strconv.Atoi(c.config.ID)
	if err != nil {
		log.Criticalf("action: create_bet | result: fail | client_id: %v | error: Invalid agency id %v",
			c.config.ID,
			err,
		)
		return
	}

	bets, err := utils.ReadBetCSV(c.config.CsvFilename, agency)
	if err != nil {
		log.Criticalf("action: read_csv | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}

	for _, bet := range bets {
		select {
		case <-terminateChan:
			log.Infof("action: sigterm_signal | result: success | client_id: %v", c.config.ID)
			return
		default:
			payloadBytes := bet.ToBytes()

			// Check if batcher is full
			// TODO - Handle batcher too small
			if c.batcher.IsFullWithNewItem(payloadBytes) {
				msg := protocol.Message{
					Identifier: protocol.Identifier{Type: protocol.IdentifierTypeMessage},
					MsgType:    protocol.MsgTypeSendBet,
					Size:       len(c.batcher.ToBytes()),
					Payload:    c.batcher.ToBytes(),
				}
				err = utils.WriteToSocket(conn, msg.ToBytes())
				if err != nil {
					log.Criticalf(
						"action: send_bet | result: fail | client_id: %v | error: %v",
						c.config.ID,
						err,
					)
					return
				}

				response := protocol.ResponseFlag{}
				err = response.FromSocket(&conn)
				if err != nil {
					log.Criticalf(
						"action: response_bet | result: fail | client_id: %v | error: %v",
						c.config.ID,
						err,
					)
					return
				}

				log.Infof("action: send_bet | result: success | client_id: %v | number_of_bets: %v",
					c.config.ID,
					c.batcher.Counter,
				)
				c.batcher.Reset()
			} else {
				err = c.batcher.Add(payloadBytes)
				// this shouldn't happen
				if err != nil {
					log.Criticalf(
						"action: send_bet | result: fail | client_id: %v | error: %v",
						c.config.ID,
						err,
					)
				}
			}
		}
	}

	flag := protocol.ResponseFlag{
		Identifier: protocol.Identifier{Type: protocol.IdentifierTypeFlag},
		FlagType:   protocol.FlagTypeEND,
	}

	err = utils.WriteToSocket(conn, flag.ToBytes())
	if err != nil {
		log.Criticalf(
			"action: send_end | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}

	log.Infof("action: send_end | result: success | client_id: %v", c.config.ID)
}
