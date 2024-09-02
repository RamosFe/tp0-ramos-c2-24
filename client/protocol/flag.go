package protocol

import (
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/utils"
	"net"
)

type FlagType int

const (
	OK    FlagType = iota
	ERROR FlagType = iota
)

const (
	FlagTypeSize = 1
)

type ResponseFlag struct {
	FlagType FlagType
}

func (r *ResponseFlag) ToBytes() []byte {
	flagTypeBuf := []byte{byte(r.FlagType)}

	return flagTypeBuf
}

func (r *ResponseFlag) FromSocket(conn *net.Conn) error {
	flagTypeBuf := make([]byte, FlagTypeSize)
	err := utils.ReadFromSocket(*conn, &flagTypeBuf, FlagTypeSize)
	if err != nil {
		return err
	}

	r.FlagType = FlagType(flagTypeBuf[0])
	return nil
}
