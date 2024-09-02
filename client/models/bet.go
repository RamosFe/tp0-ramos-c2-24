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
	Name          string
	Lastname      string
	Document      int
	Birthday      string
	LotteryNumber int
	Agency        int
}

// GetFromEnv retrieves the Bet fields from environment variables
// and populates the Bet struct. Returns an error if parsing fails.
func (b *Bet) GetFromEnv(agency int) error {
	name := os.Getenv(EnvNameField)
	surname := os.Getenv(EnvSurnameField)
	documentStr := os.Getenv(EnvDocumentField)
	birthdayStr := os.Getenv(EnvBirthdayField)
	ticketNumberStr := os.Getenv(EnvTicketNumberField)

	document, err := strconv.ParseUint(documentStr, 10, 32)
	if err != nil {
		return fmt.Errorf("failed to parse Document: %w", err)
	}

	ticketNumber, err := strconv.ParseUint(ticketNumberStr, 10, 32)
	if err != nil {
		return fmt.Errorf("failed to parse ticket number: %w", err)
	}

	b.Name = name
	b.Lastname = surname
	b.Document = int(document)
	b.Birthday = birthdayStr
	b.LotteryNumber = int(ticketNumber)
	b.Agency = agency

	return nil
}

// ToString converts the Bet struct to a string with fields
// separated by a defined separator.
func (b *Bet) ToString() string {
	return b.Name + BetStringSeparator +
		b.Lastname + BetStringSeparator +
		strconv.Itoa(b.Document) + BetStringSeparator +
		b.Birthday + BetStringSeparator +
		strconv.Itoa(b.LotteryNumber) + BetStringSeparator +
		strconv.Itoa(b.Agency)
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
		return fmt.Errorf("invalid Document: not an integer - %s", parts[2])
	}

	lotteryNumber, err := strconv.Atoi(parts[4])
	if err != nil {
		return fmt.Errorf("invalid lottery number: not an integer - %s", parts[4])
	}

	agency, err := strconv.Atoi(parts[5])
	if err != nil {
		return fmt.Errorf("invalid agency number: not an integer - %s", parts[5])
	}

	b.Name = parts[0]
	b.Lastname = parts[1]
	b.Document = document
	b.Birthday = parts[3]
	b.LotteryNumber = lotteryNumber
	b.Agency = agency

	return nil
}

// ToBytes converts the Bet struct to a byte slice using the ToString
// representation of the Bet.
func (b *Bet) ToBytes() []byte {
	return []byte(b.ToString())
}
