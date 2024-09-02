package protocol

import (
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/utils"
	"net"
)

const (
	TypeSize = 1
)

type Type int

const (
	IdentifierTypeMessage Type = iota
	IdentifierTypeFlag    Type = iota
)

type Identifier struct {
	Type Type
}

func (i *Identifier) ToBytes() []byte {
	protocolTypeBuf := []byte{byte(i.Type)}
	return protocolTypeBuf
}

func (i *Identifier) FromSocket(conn *net.Conn) error {
	protocolTypeBuf := make([]byte, TypeSize)
	err := utils.ReadFromSocket(*conn, &protocolTypeBuf, TypeSize)
	if err != nil {
		return err
	}

	i.Type = Type(protocolTypeBuf[0])

	return nil
}
