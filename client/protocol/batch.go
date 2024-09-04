package protocol

import (
	"bytes"
	"fmt"
)

const MaxBytesLimit = 8000

var FullBatcherError error = fmt.Errorf("the batcher is full")

type Batcher struct {
	MaxLimit int
	Counter  int
	buffer   bytes.Buffer
}

func NewBatcher(maxBytesLimit int) *Batcher {
	return &Batcher{
		maxBytesLimit,
		0,
		bytes.Buffer{},
	}
}

func (b *Batcher) IsFull() bool {
	if b.Counter > b.MaxLimit {
		return true
	}

	return false
}

func (b *Batcher) IsEmpty() bool {
	return b.Counter == 0 && b.buffer.Len() == 0
}

func (b *Batcher) IsFullWithNewItem(message []byte) bool {
	if b.buffer.Len()+len(message) > MaxBytesLimit || b.Counter+1 > b.MaxLimit {
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
