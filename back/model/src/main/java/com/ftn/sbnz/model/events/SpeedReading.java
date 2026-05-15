package com.ftn.sbnz.model.events;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.kie.api.definition.type.Expires;
import org.kie.api.definition.type.Role;
import org.kie.api.definition.type.Timestamp;

import java.util.Date;

@Role(Role.Type.EVENT)
@Timestamp("timestamp")
@Expires("5m")

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SpeedReading {
    private double speed;           // m/s
    private Date timestamp;

    public SpeedReading(double speed) {
        this.speed = speed;
        this.timestamp = new Date();
    }
}
