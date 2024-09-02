package protocol

import (
	"encoding/binary"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/utils"
	"net"
)

type MessageType int

const (
	SendBet MessageType = iota
)

const (
	MsgTypeSize = 1
	HeaderSize  = 2
)

type Message struct {
	MsgType MessageType
	Size    int
	Payload []byte
}

func (m *Message) ToBytes() []byte {
	msgTypeBuf := []byte{byte(m.MsgType)}

	headerBuf := make([]byte, HeaderSize)
	binary.BigEndian.PutUint16(headerBuf, uint16(m.Size))

	return append(append(msgTypeBuf, headerBuf...), m.Payload...)
}

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

	m.MsgType = MessageType(binary.BigEndian.Uint16(payloadBuf))
	m.Size = int(binary.BigEndian.Uint16(sizeBuf))
	m.Payload = payloadBuf

	return nil
}
