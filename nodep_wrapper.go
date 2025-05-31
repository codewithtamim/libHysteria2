package libHysteria2

import (
	"github.com/CodeWithTamim/libHysteria2/nodep"
)

func GetFreePorts(count int) ([]int, error) {
	return nodep.GetFreePorts(count)
}

func ConvBandwidth(bw interface{}) (uint64, error) {
	return nodep.ConvBandwidth(bw)
}

func StringToBps(s string) (uint64, error) {
	return nodep.StringToBps(s)
}
