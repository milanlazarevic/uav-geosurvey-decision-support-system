package com.ftn.sbnz.service;


import com.ftn.sbnz.model.decisions.FlightDecision;
import com.ftn.sbnz.model.events.*;
import com.ftn.sbnz.model.enums.*;
import com.ftn.sbnz.model.facts.FlightFact;
import com.ftn.sbnz.model.facts.FlightWarning;
import org.kie.api.KieBase;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;
import org.kie.api.runtime.rule.FactHandle;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

@Service
public class FlightDecisionService {

    private static final Logger log = LoggerFactory.getLogger(FlightDecisionService.class);

    private final KieBase kieBase;
    private KieSession cepSession;

    @Autowired
    public FlightDecisionService(KieBase kieContainer) {
        this.kieBase = kieContainer;
    }

    @PostConstruct
    public void initSession() {
        log.info("Initializing UAV CEP session...");
        cepSession = kieBase.newKieSession();

        if (cepSession == null) {
            throw new RuntimeException("Failed to create uavCepSession! Check kmodule.xml");
        }

        log.info("UAV CEP session initialized. Session ID: {}", cepSession.getIdentifier());
    }

    /**
     * Process telemetry event through CEP session
     */
    public FlightDecision processTelemetry(
            BatteryReading battery,
            SignalReading signal,
            SpeedReading speed,
            GnssReading gnss) {

        log.debug("Processing telemetry: Battery={}%, Signal={}%, Speed={}m/s, GNSS Sats={}",
                battery.getLevel(), signal.getStrength(), speed.getSpeed(), gnss.getSatellites());

        // Insert all events
        cepSession.insert(battery);
        cepSession.insert(signal);
        cepSession.insert(speed);
        cepSession.insert(gnss);

        // Fire rules
        int rulesFired = cepSession.fireAllRules();
        log.debug("Rules fired: {}", rulesFired);

        // Extract decision
        FlightDecision decision = getLatestDecision();

        // Log all warnings
        Collection<FlightWarning> warnings = getActiveWarnings();
        warnings.forEach(w -> log.info("Warning: {}", w.getMessage()));

        return decision;
    }

    /**
     * Process single event (for individual telemetry updates)
     */
    public FlightDecision processEvent(Object event) {
        cepSession.insert(event);
        int rulesFired = cepSession.fireAllRules();
        log.debug("Event processed. Rules fired: {}", rulesFired);

        return getLatestDecision();
    }

    /**
     * Get the latest flight decision from working memory
     */
    public FlightDecision getLatestDecision() {
        Collection<?> objects = cepSession.getObjects(obj -> obj instanceof FlightDecision);

        if (objects.isEmpty()) {
            return new FlightDecision(
                    FlightState.SAFE,
                    Action.CONTINUE,
                    "No decision made yet"
            );
        }

        // Return most recent decision
        return objects.stream()
                .map(obj -> (FlightDecision) obj)
                .max((d1, d2) -> Long.compare(d1.getTimestamp(), d2.getTimestamp()))
                .orElse(null);
    }

    /**
     * Get all active warnings
     */
    public Collection<FlightWarning> getActiveWarnings() {
        Collection<?> objects = cepSession.getObjects(obj -> obj instanceof FlightWarning);
        List<FlightWarning> warnings = new ArrayList<>();

        for (Object obj : objects) {
            warnings.add((FlightWarning) obj);
        }

        return warnings;
    }

    /**
     * Get all flight facts (for debugging)
     */
    public Collection<FlightFact> getFlightFacts() {
        Collection<?> objects = cepSession.getObjects(obj -> obj instanceof FlightFact);
        List<FlightFact> facts = new ArrayList<>();

        for (Object obj : objects) {
            facts.add((FlightFact) obj);
        }

        return facts;
    }

    /**
     * Clear all decisions and warnings (useful for reset)
     */
    public void clearDecisions() {

        Collection<FactHandle> allFacts =
                cepSession.getFactHandles();

        int count = allFacts.size();

        allFacts.forEach(cepSession::delete);

        log.info("Cleared {} objects from CEP session", count);
    }

    @PreDestroy
    public void cleanup() {
        if (cepSession != null) {
            log.info("Disposing UAV CEP session...");
            cepSession.dispose();
        }
    }

    public KieSession getCepSession() {
        return cepSession;
    }
}
