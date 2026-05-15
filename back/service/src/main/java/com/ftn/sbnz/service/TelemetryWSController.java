package com.ftn.sbnz.service;

import com.ftn.sbnz.model.decisions.FlightDecision;
import com.ftn.sbnz.model.enums.FixType;
import com.ftn.sbnz.model.events.BatteryReading;
import com.ftn.sbnz.model.events.GnssReading;
import com.ftn.sbnz.model.events.SignalReading;
import com.ftn.sbnz.model.events.SpeedReading;
import com.ftn.sbnz.model.facts.FlightFact;
import com.ftn.sbnz.model.facts.FlightWarning;
import com.ftn.sbnz.service.dto.TelemetryRequest;
import lombok.AllArgsConstructor;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

@Controller
@AllArgsConstructor
public class TelemetryWSController {

    private final FlightDecisionService decisionService;
    private final SimpMessagingTemplate messagingTemplate;



    @MessageMapping("/telemetry")
    public void processTelemetry(TelemetryRequest request) {

        BatteryReading battery = new BatteryReading(request.getBattery());

        SignalReading signal = new SignalReading(request.getSignal());

        SpeedReading speed = new SpeedReading(request.getSpeed());

        GnssReading gnss = new GnssReading(
                request.getHdop(),
                request.getSatellites(),
                FixType.valueOf(request.getFixType())
        );

        FlightDecision decision =
                decisionService.processTelemetry(
                        battery,
                        signal,
                        speed,
                        gnss
                );

        Collection<FlightWarning> warnings =
                decisionService.getActiveWarnings();

        Collection<FlightFact> facts =
                decisionService.getFlightFacts();

        Map<String, Object> response = new HashMap<>();

        response.put("decision", decision);
        response.put("warnings", warnings);
        response.put("facts", facts);
        response.put("battery", battery);
        response.put("signal", signal);
        response.put("speed", speed);
        response.put("gnss", gnss);

        messagingTemplate.convertAndSend(
                "/topic/telemetry",
                response
        );
    }
}
