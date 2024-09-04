package protocol

import (
	"bytes"
	"encoding/binary"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/utils"
	"net"
)

type MessageType int

const (
	// MsgTypeSendBet represents a type used for messages that sends bets
	MsgTypeSendBet MessageType = iota
)

const (
	// MsgTypeSize represent the size in bytes of the MsgType
	MsgTypeSize = 1
	// HeaderSize represent the size in bytes of the Header
	HeaderSize = 2
)

// Message represents a message that contains a variable-size payload
type Message struct {
	Identifier Identifier
	// MsgType represents the type of the message
	MsgType MessageType
	// Size represents the size of the payload
	Size int
	// Payload holds the actual data of the message
	Payload []byte
}

// ToBytes converts the Message to a byte slice.
func (m *Message) ToBytes() []byte {
	identifierBuf := m.Identifier.ToBytes()
	msgTypeBuf := []byte{byte(m.MsgType)}

	headerBuf := make([]byte, HeaderSize)
	binary.BigEndian.PutUint16(headerBuf, uint16(m.Size))

	buffer := bytes.Buffer{}
	buffer.Write(identifierBuf)
	buffer.Write(msgTypeBuf)
	buffer.Write(headerBuf)
	buffer.Write(m.Payload)
	return buffer.Bytes()
}

// FromSocket initializes the Message by reading data from a socket.
func (m *Message) FromSocket(conn *net.Conn) error {
	msgTypeBuf := make([]byte, MsgTypeSize)
	err := utils.ReadFromSocket(*conn, &msgTypeBuf, MsgTypeSize)
	if err != nil {
		return err
	}

	sizeBuf := make([]byte, HeaderSize)
	err = utils.ReadFromSocket(*conn, &sizeBuf, HeaderSize)
	if err != nil {
		return err
	}

	payloadBuf := make([]byte, binary.BigEndian.Uint16(sizeBuf))
	err = utils.ReadFromSocket(*conn, &payloadBuf, MsgTypeSize)
	if err != nil {
		return err
	}

	m.Identifier = Identifier{IdentifierTypeMessage}
	m.MsgType = MessageType(msgTypeBuf[0])
	m.Size = int(binary.BigEndian.Uint16(sizeBuf))
	m.Payload = payloadBuf

	return nil
}
