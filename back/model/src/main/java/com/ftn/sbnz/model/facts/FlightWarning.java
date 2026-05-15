package com.ftn.sbnz.model.facts;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.kie.api.definition.type.Role;
import org.kie.api.definition.type.Timestamp;

@Role(Role.Type.EVENT)
@Timestamp("timestamp")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class FlightWarning {
    private String message;
    private long timestamp;

    public FlightWarning(String message) {
        this.message = message;
        this.timestamp = System.currentTimeMillis();
    }
}