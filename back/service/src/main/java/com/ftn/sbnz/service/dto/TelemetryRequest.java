package com.ftn.sbnz.service.dto;

import lombok.Data;

@Data
public class TelemetryRequest {
    private double battery;
    private int signal;
    private double speed;
    private double hdop;
    private int satellites;
    private String fixType;
}
