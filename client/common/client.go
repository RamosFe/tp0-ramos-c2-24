package common

import (
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/models"
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
	agency  int
}

// NewClient Initializes a new client with the given configuration
func NewClient(config ClientConfig) *Client {
	agency, err := strconv.Atoi(config.ID)
	if err != nil {
		log.Fatalf("Error parsing agency id %s: %s", config.ID, err)
		return nil
	}

	return &Client{
		config:  config,
		batcher: *protocol.NewBatcher(config.BatchMaxAmount),
		agency:  agency,
	}
}

// LogError Logs an error message with the specified action
func (c *Client) LogError(action string, err error) {
	log.Criticalf(
		"action: %s | result: fail | client_id: %v | error: %v",
		action,
		c.config.ID,
		err,
	)
}

// SendBatch Sends the current batch of bets to the server
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

// SendAllBets Reads bets from CSV and sends them to the server
func (c *Client) SendAllBets(terminateChan chan os.Signal) error {
	conn, err := net.Dial("tcp", c.config.ServerAddress)
	if err != nil {
		c.LogError("connect", err)
		return err
	}
	defer conn.Close()

	bets, err := utils.ReadBetCSV(c.config.CsvFilename, c.agency)
	if err != nil {
		c.LogError("read_csv", err)
		return err
	}

	for _, bet := range bets {
		select {
		case <-terminateChan:
			log.Infof("action: sigterm_signal | result: success | client_id: %v", c.config.ID)
			return nil
		default:
			payloadBytes := bet.ToBytes()

			// Checks if batcher is full
			if c.batcher.IsFullWithNewItem(payloadBytes) {
				if err := c.SendBatch(&conn); err != nil {
					return err
				}
			}

			if err := c.batcher.Add(payloadBytes); err != nil {
				c.LogError("send_bet", err)
				return err
			}
		}
	}

	if !c.batcher.IsEmpty() {
		if err := c.SendBatch(&conn); err != nil {
			return err
		}
	}

	flag := protocol.ResponseFlag{
		Identifier: protocol.Identifier{Type: protocol.IdentifierTypeFlag},
		FlagType:   protocol.FlagTypeEND,
	}

	if err = utils.WriteToSocket(conn, flag.ToBytes()); err != nil {
		c.LogError("send_end", err)
		return err
	}

	log.Infof("action: send_end | result: success | client_id: %v", c.config.ID)
	return nil
}

// AskForWinner Requests winners from the server with retries
func (c *Client) AskForWinner(terminateChan chan os.Signal) error {
	maxNumberOfRetries := 5
	timeBetweenRestries := 4

	for i := 0; i < maxNumberOfRetries; i++ {
		select {
		case <-terminateChan:
			log.Infof("action: sigterm_signal | result: success | client_id: %v", c.config.ID)
			return nil
		default:
			{
				conn, err := net.Dial("tcp", c.config.ServerAddress)
				if err != nil {
					c.LogError("connect", err)
					return err
				}

				askWinners := models.AskWinner{AgencyId: c.agency}
				msg := protocol.Message{
					Identifier: protocol.Identifier{Type: protocol.IdentifierTypeMessage},
					MsgType:    protocol.MsgTypeAskWinners,
					Size:       len(askWinners.ToBytes()),
					Payload:    askWinners.ToBytes(),
				}
				if err := utils.WriteToSocket(conn, msg.ToBytes()); err != nil {
					c.LogError("ask_winners", err)
					conn.Close()
					return err
				}

				identifier := protocol.Identifier{}
				if er := identifier.FromSocket(&conn); er != nil {
					c.LogError("recv_winners", err)
					conn.Close()
					return err
				}

				if identifier.Type == protocol.IdentifierTypeMessage {
					response := protocol.Message{}
					if err := response.FromSocket(&conn); err != nil {
						c.LogError("recv_winners", err)
						conn.Close()
						return err
					}
					winners := models.Winners{}
					if err := winners.FromBytes(response.Payload); err != nil {
						c.LogError("recv_winners", err)
						conn.Close()
						return err
					}

					log.Infof("action: consulta_ganadores | result: success | cant_ganadores: %v}",
						len(winners.Documents),
					)
					conn.Close()
					return nil
				} else if identifier.Type == protocol.IdentifierTypeFlag {
					response := protocol.ResponseFlag{}
					if err := response.FromSocket(&conn); err != nil {
						c.LogError("recv_winners", err)
						conn.Close()
						return err
					}
					log.Infof("action: recv_winners | result: not-available | msg: waiting %v seconds for retry",
						timeBetweenRestries,
					)
					conn.Close()
					time.Sleep(time.Duration(timeBetweenRestries) * time.Second)
				}
			}
		}
	}

	log.Infof("action: send_end | result: max-retries | msg: max retries reached")
	return nil
}

// StartClientLoop Starts the client loop to send bets and request winners
func (c *Client) StartClientLoop(terminateChan chan os.Signal) {
	if err := c.SendAllBets(terminateChan); err != nil {
		return
	}

	if err := c.AskForWinner(terminateChan); err != nil {
		return
	}
}
