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
	ID            string
	ServerAddress string
	LoopAmount    int
	LoopPeriod    time.Duration
}

type Client struct {
	config ClientConfig
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	return &Client{config: config}
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

	select {
	case <-terminateChan:
		log.Infof("action: sigterm_signal | result: success | client_id: %v", c.config.ID)
		return
	default:
		bet := models.Bet{}
		agency, err := strconv.Atoi(c.config.ID)
		if err != nil {
			log.Criticalf("action: create_bet | result: fail | client_id: %v | error: Invalid agency id %v",
				c.config.ID,
				err,
			)
			return
		}
		err = bet.GetFromEnv(agency)
		if err != nil {
			log.Criticalf(
				"action: create_bet | result: fail | client_id: %v | error: %v",
				c.config.ID,
				err,
			)
			return
		}

		payloadBytes := bet.ToBytes()
		msg := protocol.Message{
			MsgType: protocol.SendBet,
			Size:    len(payloadBytes),
			Payload: payloadBytes,
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

		log.Infof("action: apuesta_enviada | result: success | dni: %v | numero: %v",
			bet.Document,
			bet.LotteryNumber,
		)
	}
}
