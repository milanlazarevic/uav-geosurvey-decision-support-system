package com.ftn.sbnz.model.events;

import com.ftn.sbnz.model.enums.FixType;
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
public class GnssReading {
    private double hdop;            // Horizontal Dilution of Precision
    private int satellites;         // Number of satellites
    private FixType fixType;        // NONE, 2D, 3D, RTK
    private Date timestamp;

    public GnssReading(double hdop, int satellites, FixType fixType) {
        this.hdop = hdop;
        this.satellites = satellites;
        this.fixType = fixType;
        this.timestamp = new Date();
    }
}
