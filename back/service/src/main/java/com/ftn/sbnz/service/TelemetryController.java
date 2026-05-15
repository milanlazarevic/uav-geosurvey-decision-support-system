package com.ftn.sbnz.service;


import com.ftn.sbnz.model.decisions.FlightDecision;
import com.ftn.sbnz.model.enums.FixType;
import com.ftn.sbnz.model.events.*;
import com.ftn.sbnz.model.facts.FlightFact;
import com.ftn.sbnz.model.facts.FlightWarning;
import com.ftn.sbnz.service.dto.TelemetryRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.web.bind.annotation.*;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/telemetry")
public class TelemetryController {

    private final FlightDecisionService decisionService;

    @Autowired
    public TelemetryController(FlightDecisionService decisionService) {
        this.decisionService = decisionService;
    }
    /**
     * Process complete telemetry packet
     * POST /api/telemetry
     * Body: {
     *   "battery": 15.0,
     *   "signal": 20,
     *   "speed": 12.5,
     *   "hdop": 4.2,
     *   "satellites": 6,
     *   "fixType": "FIX_3D"
     * }
     */
    @PostMapping
    public Map<String, Object> processTelemetry(@RequestBody TelemetryRequest request) {

        BatteryReading battery = new BatteryReading(request.getBattery());
        SignalReading signal = new SignalReading(request.getSignal());
        SpeedReading speed = new SpeedReading(request.getSpeed());
        GnssReading gnss = new GnssReading(
                request.getHdop(),
                request.getSatellites(),
                FixType.valueOf(request.getFixType())
        );

        FlightDecision decision = decisionService.processTelemetry(battery, signal, speed, gnss);

        Collection<FlightWarning> warnings = decisionService.getActiveWarnings();
        Collection<FlightFact> facts = decisionService.getFlightFacts();

        Map<String, Object> response = new HashMap<>();
        response.put("decision", decision);
        response.put("warnings", warnings);
        response.put("facts", facts);

        return response;
    }

    /**
     * Process battery reading only
     * POST /api/telemetry/battery?level=15.0
     */
    @PostMapping("/battery")
    public FlightDecision processBattery(@RequestParam double level) {
        BatteryReading reading = new BatteryReading(level);
        return decisionService.processEvent(reading);
    }

    /**
     * Process signal reading only
     * POST /api/telemetry/signal?strength=20
     */
    @PostMapping("/signal")
    public FlightDecision processSignal(@RequestParam int strength) {
        SignalReading reading = new SignalReading(strength);
        return decisionService.processEvent(reading);
    }

    /**
     * Get current flight status
     */
    @GetMapping("/status")
    public Map<String, Object> getStatus() {
        FlightDecision decision = decisionService.getLatestDecision();
        Collection<FlightWarning> warnings = decisionService.getActiveWarnings();
        Collection<FlightFact> facts = decisionService.getFlightFacts();

        Map<String, Object> status = new HashMap<>();
        status.put("decision", decision);
        status.put("warnings", warnings);
        status.put("facts", facts);
        status.put("warningCount", warnings.size());
        status.put("factCount", facts.size());

        return status;
    }

    /**
     * Clear all decisions and facts (reset)
     */
    @PostMapping("/reset")
    public String reset() {
        decisionService.clearDecisions();
        return "Session cleared";
    }
}