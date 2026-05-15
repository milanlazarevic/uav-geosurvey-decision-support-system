package com.ftn.sbnz.model.facts;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class FlightFact {
    private String value;           // e.g., "BATTERY_LOW", "SIGNAL_WEAK" TODO make this enum
    private long timestamp;

    public FlightFact(String value) {
        this.value = value;
        this.timestamp = System.currentTimeMillis();
    }
}