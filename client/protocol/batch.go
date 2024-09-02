package protocol

import (
	"bytes"
	"fmt"
)

var FullBatcherError error = fmt.Errorf("the batcher is full")

type Batcher struct {
	MaxBytesLimit int
	Counter       int
	buffer        bytes.Buffer
}

func NewBatcher(maxBytesLimit int) *Batcher {
	return &Batcher{
		maxBytesLimit,
		0,
		bytes.Buffer{},
	}
}

func (b *Batcher) IsFull() bool {
	if b.buffer.Len() > b.MaxBytesLimit {
		return true
	}

	return false
}

func (b *Batcher) IsFullWithNewItem(message []byte) bool {
	if b.buffer.Len()+len(message) > b.MaxBytesLimit {
		return true
	}
	return false
}

func (b *Batcher) Add(message []byte) error {
	if b.IsFullWithNewItem(message) {
		return FullBatcherError
	}

	b.buffer.Write(message)
	b.buffer.WriteByte('\n')
	b.Counter += 1
	return nil
}

func (b *Batcher) ToBytes() []byte {
	return b.buffer.Bytes()[:b.buffer.Len()-1]
}

func (b *Batcher) Reset() {
	b.Counter = 0
	b.buffer.Reset()
}
