package libHysteria2

import (
	"github.com/CodeWithTamim/libHysteria2/hysteria2"
	"github.com/CodeWithTamim/libHysteria2/memory"
	"go.uber.org/zap"
)

func StartTunnel(configJson string) {
	memory.InitForceFree()
	hysteria2.StartTunnel(configJson)
}

func StopTunnel() {
	hysteria2.StopTunnel()
}

func GetCoreState() bool {
	return hysteria2.GetCoreState()
}

func TestConfig(configJson string) error {
	return hysteria2.TestConfig(configJson)
}

func SetLogger(customLogger *zap.Logger) {
	hysteria2.SetLogger(customLogger)
}

func DisableLogging() {
	hysteria2.DisableLogging()
}

func EnableDefaultLogging() {
	hysteria2.EnableDefaultLogging()
}
