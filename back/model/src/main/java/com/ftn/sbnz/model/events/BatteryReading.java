package com.ftn.sbnz.model.events;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.kie.api.definition.type.*;
import java.util.Date;

@Role(Role.Type.EVENT)
@Timestamp("timestamp")
@Expires("5m")

@Data
@NoArgsConstructor
@AllArgsConstructor
public class BatteryReading {
    private double level;           // (0-100)
    private Date timestamp;
    public BatteryReading(double level) {
        this.level = level;
        this.timestamp = new Date();
    }
}