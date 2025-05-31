package hysteria2

import (
	"encoding/json"
	"log"

	"github.com/apernet/hysteria/core/v2/client"
	"go.uber.org/zap"
)

var (
	globalClient       client.Client
	isCoreRunning      bool
	logger             *zap.Logger
	disableUpdateCheck bool = true
)

 func init() {
	 
	var err error
	logger, err = zap.NewDevelopment()
	if err != nil {
		 
		logger, _ = zap.NewProduction()
	}
	if logger != nil {
		logger.Info("Hysteria2 logger initialized")
	}
}

 func StartTunnel(configJson string) {
	if logger != nil {
		logger.Info("Starting Hysteria2 tunnel")
	}

	var config clientConfig
	if err := json.Unmarshal([]byte(configJson), &config); err != nil {
		if logger != nil {
			logger.Error("Error while unmarshaling config", zap.Error(err))
		}
		log.Fatalf("Error while unmarshaling config. %v", err)
		return
	}
	var err error

	globalClient, err = client.NewReconnectableClient(
		config.Config,
		func(c client.Client, info *client.HandshakeInfo, count int) {
			connectLog(info, count)
		},
		config.Lazy,
	)

	if err != nil {
		if logger != nil {
			logger.Error("Error while starting client", zap.Error(err))
		}
		log.Fatalf("Error while starting client. %v", err)
		return
	}
	isCoreRunning = true

	if logger != nil {
		logger.Info("Hysteria2 tunnel started successfully")
	}
}

 func StopTunnel() {
	if logger != nil {
		logger.Info("Stopping Hysteria2 tunnel")
	}

	if globalClient != nil {
		_ = globalClient.Close()
		if logger != nil {
			logger.Info("Tunnel shutdown successful")
		}
	}
	isCoreRunning = false
}

 func GetCoreState() bool {
	return isCoreRunning
}

 func TestConfig(configJson string) error {
	var config clientConfig
	if err := json.Unmarshal([]byte(configJson), &config); err != nil {
		return err
	}
	_, err := config.Config()
	return err
}

func connectLog(info *client.HandshakeInfo, count int) {
	if logger != nil {
		logger.Info("connected to server",
			zap.Bool("udpEnabled", info.UDPEnabled),
			zap.Uint64("tx", info.Tx),
			zap.Int("count", count))
	}
}

func SetLogger(customLogger *zap.Logger) {
	logger = customLogger
	if logger != nil {
		logger.Info("Custom logger set for Hysteria2")
	}
}

func DisableLogging() {
	logger = nil
}

func EnableDefaultLogging() {
	var err error
	logger, err = zap.NewDevelopment()
	if err != nil {
		logger, _ = zap.NewProduction()
	}
	if logger != nil {
		logger.Info("Default logging re-enabled for Hysteria2")
	}
}
