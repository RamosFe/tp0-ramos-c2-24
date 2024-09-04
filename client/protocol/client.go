package protocol

import (
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/utils"
	"net"
)

// SendBets Sends a batch of bets to the server and receives a response flag
func SendBets(conn *net.Conn, data []byte) (*ResponseFlag, error) {
	msg := Message{
		Identifier: Identifier{Type: IdentifierTypeMessage},
		MsgType:    MsgTypeSendBet,
		Size:       len(data),
		Payload:    data,
	}
	err := utils.WriteToSocket(*conn, msg.ToBytes())
	if err != nil {
		return nil, err
	}

	identifier := Identifier{}
	err = identifier.FromSocket(conn)
	if err != nil {
		return nil, err
	}

	response := ResponseFlag{}
	err = response.FromSocket(conn)
	if err != nil {
		return nil, err
	}

	return &response, nil
}
