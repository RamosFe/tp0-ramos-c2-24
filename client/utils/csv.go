package utils

import (
	"encoding/csv"
	"fmt"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/models"
	"os"
	"strconv"
)

func ReadBetCSV(filename string, agency int) ([]models.Bet, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	var bets []models.Bet
	for i, record := range records {
		if i == 0 {
			continue
		}

		document, err := strconv.Atoi(record[2])
		if err != nil {
			return nil, fmt.Errorf("failed to parse document number: %v, err")
		}

		number, err := strconv.Atoi(record[4])
		if err != nil {
			return nil, fmt.Errorf("failed to parse bet number: %v", err)
		}

		bet := models.Bet{
			Name:          record[0],
			Lastname:      record[1],
			Document:      document,
			Birthday:      record[3],
			LotteryNumber: number,
			Agency:        agency,
		}

		bets = append(bets, bet)
	}

	return bets, nil
}
