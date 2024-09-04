package models

import (
	"strconv"
	"strings"
)

// Winners represents the result of a lottery draw, including the size and a list of winning documents.
type Winners struct {
	Size      int
	Documents []string
}

// FromBytes Parses the byte buffer to initialize the Winners struct
func (w *Winners) FromBytes(buffer []byte) error {
	decoded := strings.Split(string(buffer), ",")

	size, err := strconv.Atoi(decoded[0])
	if err != nil {
		return err
	}

	w.Size = size
	if w.Size == 0 {
		w.Documents = []string{}
	} else {
		w.Documents = decoded[1:]
	}
	return nil
}

// AskWinner represents a request to get winners for a specific agency.
type AskWinner struct {
	AgencyId int
}

// ToBytes Converts the AskWinner struct to a byte slice
func (a *AskWinner) ToBytes() []byte {
	return []byte{byte(a.AgencyId)}
}
