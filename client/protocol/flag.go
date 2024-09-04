package protocol

import (
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/utils"
	"net"
)

type FlagType int

// Define possible flag types
const (
	FlagTypeOK        FlagType = iota
	FlagTypeERROR     FlagType = iota
	FlagTypeEND       FlagType = iota
	FlagTypeNoWinners FlagType = iota
)

// FlagTypeSize Size of the FlagType field in bytes
const (
	FlagTypeSize = 1
)

// ResponseFlag Represents a response without payload
type ResponseFlag struct {
	Identifier Identifier
	// FlagType represents the type of the response flag
	FlagType FlagType
}

// ToBytes converts the ResponseFlag to a byte slice.
func (r *ResponseFlag) ToBytes() []byte {
	identifierBuf := r.Identifier.ToBytes()
	flagTypeBuf := []byte{byte(r.FlagType)}
	return append(identifierBuf, flagTypeBuf...)
}

// FromSocket initializes the ResponseFlag by reading data from a socket.
func (r *ResponseFlag) FromSocket(conn *net.Conn) error {
	flagTypeBuf := make([]byte, FlagTypeSize)
	err := utils.ReadFromSocket(*conn, &flagTypeBuf, FlagTypeSize)
	if err != nil {
		return err
	}

	r.Identifier = Identifier{IdentifierTypeFlag}
	r.FlagType = FlagType(flagTypeBuf[0])
	return nil
}
