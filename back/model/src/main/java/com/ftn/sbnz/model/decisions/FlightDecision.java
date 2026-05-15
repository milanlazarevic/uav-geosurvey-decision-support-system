package com.ftn.sbnz.model.decisions;


import com.ftn.sbnz.model.enums.Action;
import com.ftn.sbnz.model.enums.FlightState;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class FlightDecision {
    private FlightState state;
    private Action action;
    private String reason;
    private long timestamp;

    public FlightDecision(FlightState state, Action action, String reason) {
        this.state = state;
        this.action = action;
        this.reason = reason;
        this.timestamp = System.currentTimeMillis();
    }
}