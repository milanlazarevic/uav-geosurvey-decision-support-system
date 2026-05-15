package com.ftn.sbnz.service.tests;


import com.ftn.sbnz.model.decisions.FlightDecision;
import com.ftn.sbnz.model.enums.*;
import com.ftn.sbnz.model.events.*;
import com.ftn.sbnz.model.facts.FlightFact;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.kie.api.KieServices;
import org.kie.api.builder.Message;
import org.kie.api.builder.Results;
import org.kie.api.definition.KiePackage;
import org.kie.api.definition.rule.Rule;
import org.kie.api.event.rule.DebugAgendaEventListener;
import org.kie.api.event.rule.MatchCreatedEvent;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;

import java.util.Collection;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.*;

public class CEPPatternsTest {

    private KieServices kieServices;
    private KieContainer kieContainer;
    private KieSession kieSession;

    @BeforeEach
    public void setup() {
        kieServices = KieServices.Factory.get();
        kieContainer = kieServices.getKieClasspathContainer();
        kieSession = kieContainer.newKieSession("uavCepSession");
        Results results = kieContainer.verify();
        if (results.hasMessages(Message.Level.ERROR)) {
            results.getMessages().forEach(msg -> System.out.println(msg.getText()));
            fail("Postoje greške u pravilima!");
        }
    }

    @AfterEach
    public void cleanup() {
        if (kieSession != null) {
            kieSession.dispose();
        }
    }

    @Test
    public void testBatteryLowDetection() {
        // Insert low battery reading
        BatteryReading battery = new BatteryReading(15);
        kieSession.insert(battery);

        int rulesFired = kieSession.fireAllRules();


        assertTrue(rulesFired > 0, "At least one rule should fire");

        // Check for BATTERY_LOW fact
        Collection<?> facts = kieSession.getObjects(obj ->
                obj instanceof FlightFact &&
                        ((FlightFact) obj).getValue().equals("BATTERY_LOW")
        );

        assertEquals(1, facts.size(), "BATTERY_LOW fact should be inserted");
    }


    @Test
    public void testRapidBatteryDrainCEP() throws InterruptedException {
        // Insert first battery reading: 50%
        BatteryReading battery1 = new BatteryReading(50);
        kieSession.insert(battery1);
        kieSession.fireAllRules();

        // Wait 5 seconds
        Thread.sleep(5000);

        // Insert second battery reading: 35% (drop of 15% in 5s)
        BatteryReading battery2 = new BatteryReading(35);
        kieSession.insert(battery2);
        int rulesFired = kieSession.fireAllRules();

        // Check for BATTERY_DRAIN_RAPID fact
        Collection<?> facts = kieSession.getObjects(obj ->
                obj instanceof FlightFact &&
                        ((FlightFact) obj).getValue().equals("BATTERY_DRAIN_RAPID")
        );

        assertEquals(1, facts.size(), "BATTERY_DRAIN_RAPID should be detected");
    }

    @Test
    public void testSignalLostLandDecision() {
        // Insert signal lost
        SignalReading signal = new SignalReading(0);
        kieSession.insert(signal);

        kieSession.fireAllRules();

        // Check for LAND decision
        Collection<?> decisions = kieSession.getObjects(obj ->
                obj instanceof FlightDecision &&
                        ((FlightDecision) obj).getAction() == Action.LAND
        );

        assertEquals(1, decisions.size(), "LAND decision should be made");

        FlightDecision decision = (FlightDecision) decisions.iterator().next();
        assertEquals(FlightState.CRITICAL, decision.getState());
    }

    @Test
    public void testRiskyFlightCompositeCondition() {
        // Insert low battery
        BatteryReading battery = new BatteryReading(18);
        kieSession.insert(battery);
        kieSession.fireAllRules();

        // Insert weak signal
        SignalReading signal = new SignalReading(20);
        kieSession.insert(signal);
        int rulesFired = kieSession.fireAllRules();

        // Check for FLIGHT_RISKY fact
        Collection<?> facts = kieSession.getObjects(obj ->
                obj instanceof FlightFact &&
                        ((FlightFact) obj).getValue().equals("FLIGHT_RISKY")
        );

        assertEquals(1, facts.size(), "FLIGHT_RISKY should be detected");

        // Check for RETURN_HOME decision
        Collection<?> decisions = kieSession.getObjects(obj ->
                obj instanceof FlightDecision &&
                        ((FlightDecision) obj).getAction() == Action.RETURN_TO_HOME
        );

        assertTrue(decisions.size() > 0, "RETURN_HOME decision should be made");
    }

    @Test
    public void testSafeFlightContinue() {
        // Insert all good readings
        kieSession.insert(new BatteryReading(80));
        kieSession.insert(new SignalReading(90));
        kieSession.insert(new SpeedReading(10));
        kieSession.insert(new GnssReading(1.5, 10, FixType.FIX_3D));

        kieSession.fireAllRules();

        // Check for CONTINUE decision
        Collection<?> decisions = kieSession.getObjects(obj ->
                obj instanceof FlightDecision &&
                        ((FlightDecision) obj).getAction() == Action.CONTINUE
        );

        assertEquals(1, decisions.size(), "CONTINUE decision should be made");

        FlightDecision decision = (FlightDecision) decisions.iterator().next();
        assertEquals(FlightState.SAFE, decision.getState());
    }
}
