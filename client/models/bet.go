package models

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

const (
	EnvNameField         = "NOMBRE"
	EnvSurnameField      = "APELLIDO"
	EnvDocumentField     = "DOCUMENTO"
	EnvBirthdayField     = "NACIMIENTO"
	EnvTicketNumberField = "NUMERO"
)

const BetStringSeparator = ","

type Bet struct {
	name          string
	lastname      string
	document      int
	birthday      string
	lotteryNumber int
}

// GetFromEnv retrieves the Bet fields from environment variables
// and populates the Bet struct. Returns an error if parsing fails.
func (b *Bet) GetFromEnv() error {
	name := os.Getenv(EnvNameField)
	surname := os.Getenv(EnvSurnameField)
	documentStr := os.Getenv(EnvDocumentField)
	birthdayStr := os.Getenv(EnvBirthdayField)
	ticketNumberStr := os.Getenv(EnvTicketNumberField)

	document, err := strconv.ParseUint(documentStr, 10, 32)
	if err != nil {
		return fmt.Errorf("failed to parse document: %w", err)
	}

	ticketNumber, err := strconv.ParseUint(ticketNumberStr, 10, 32)
	if err != nil {
		return fmt.Errorf("failed to parse ticket number: %w", err)
	}

	b.name = name
	b.lastname = surname
	b.document = int(document)
	b.birthday = birthdayStr
	b.lotteryNumber = int(ticketNumber)

	return nil
}

// ToString converts the Bet struct to a string with fields
// separated by a defined separator.
func (b *Bet) ToString() string {
	return b.name + BetStringSeparator +
		b.lastname + BetStringSeparator +
		strconv.Itoa(b.document) + BetStringSeparator +
		b.birthday + BetStringSeparator +
		strconv.Itoa(b.lotteryNumber) + BetStringSeparator
}

// FromBytes parses a byte slice into a Bet struct. Returns an
// error if the input format is invalid or fields are not parsable.
func (b *Bet) FromBytes(buffer []byte) error {
	data := string(buffer)
	parts := strings.Split(data, BetStringSeparator)

	if len(parts) != 5 {
		return fmt.Errorf("invalid Bet format: %s", data)
	}

	document, err := strconv.Atoi(parts[2])
	if err != nil {
		return fmt.Errorf("invalid document: not an integer - %s", parts[2])
	}

	lotteryNumber, err := strconv.Atoi(parts[4])
	if err != nil {
		return fmt.Errorf("invalid lottery number: not an integer - %s", parts[4])
	}

	b.name = parts[0]
	b.lastname = parts[1]
	b.document = document
	b.birthday = parts[3]
	b.lotteryNumber = lotteryNumber

	return nil
}

// ToBytes converts the Bet struct to a byte slice using the ToString
// representation of the Bet.
func (b *Bet) ToBytes() []byte {
	return []byte(b.ToString())
}
