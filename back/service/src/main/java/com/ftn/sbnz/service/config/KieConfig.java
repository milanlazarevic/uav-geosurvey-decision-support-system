package com.ftn.sbnz.service.config;

import org.drools.template.ObjectDataCompiler;
import org.kie.api.KieBase;
import org.kie.api.KieBaseConfiguration;
import org.kie.api.KieServices;
import org.kie.api.builder.Message;
import org.kie.api.builder.Results;
import org.kie.api.conf.EventProcessingOption;
import org.kie.api.io.ResourceType;
import org.kie.internal.utils.KieHelper;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;

@Configuration
public class KieConfig {

    @Bean
    public KieBase kieBase() throws IOException {
        KieHelper kieHelper = new KieHelper();

        // 1. Load your static DRL files (existing rules)
        String[] drlFiles = {
                "/rules/level1/battery-rules.drl",
                "/rules/level1/gnss-rules.drl",
                "/rules/level1/signal-rules.drl",
                "/rules/level1/speed-rules.drl",
                "/rules/level2/cep-patterns.drl",
                "/rules/level2/composite-conditions.drl",
                "/rules/level3/flight-decisions.drl"
        };

        for (String path : drlFiles) {
            InputStream is = KieConfig.class.getResourceAsStream(path);
            if (is != null) {
                String content = new String(is.readAllBytes(), StandardCharsets.UTF_8);
                kieHelper.addContent(content, ResourceType.DRL);
            }
        }

        // 2. Generate rules from template + data
        List<Map<String, Object>> thresholdData = loadThresholdData();

        try (InputStream template = KieConfig.class.getResourceAsStream("/templates/threshold-template.drt")) {
            ObjectDataCompiler compiler = new ObjectDataCompiler();
            String generatedDrl = compiler.compile(thresholdData, template);
            System.out.println("=== Generated DRL ===\n" + generatedDrl); // debug
            kieHelper.addContent(generatedDrl, ResourceType.DRL);
        }

        // 3. Verify everything compiled correctly
        Results results = kieHelper.verify();
        if (results.hasMessages(Message.Level.ERROR)) {
            throw new RuntimeException("KieBase compilation failed: " +
                    results.getMessages(Message.Level.ERROR));
        }

        KieBaseConfiguration config = KieServices.Factory.get().newKieBaseConfiguration();
        config.setOption(EventProcessingOption.STREAM);
        return kieHelper.build(config);
    }

    private List<Map<String, Object>> loadThresholdData() throws IOException {
        List<Map<String, Object>> allData = new ArrayList<>();

        // List of all CSV files to load
        String[] csvFiles = {
                "/data/battery-thresholds.csv",
                "/data/gnss-thresholds.csv",
        };

        for (String csvPath : csvFiles) {
            try (InputStream is = KieConfig.class.getResourceAsStream(csvPath)) {
                if (is != null) {
                    allData.addAll(loadCsvData(is));
                    System.out.println("Loaded: " + csvPath);
                } else {
                    System.out.println("Warning: File not found - " + csvPath);
                }
            }
        }

        System.out.println("TOTAL ROWS LOADED: " + allData.size());
        for (Map<String, Object> row : allData) {
            System.out.println("ROW DATA: " + row);
        }



        return allData;
    }

    private List<Map<String, Object>> loadCsvData(InputStream is) throws IOException {
        List<Map<String, Object>> data = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(is))) {
            String headerLine = reader.readLine();
            if (headerLine == null) return data;

            String[] headers = headerLine.split(",");
            String line;

            while ((line = reader.readLine()) != null) {
                if (line.isBlank()) continue;
                String[] values = line.split(",", -1); // -1 keeps empty values

                Map<String, Object> row = new HashMap<>();
                for (int i = 0; i < headers.length && i < values.length; i++) {
                    String key = headers[i].trim();
                    String value = values[i].trim();

                    // Type conversion based on column name
                    if (key.equals("threshold")) {
                        row.put(key, Double.parseDouble(value));
                    } else if (key.equals("salience")) {
                        row.put(key, Integer.parseInt(value));
                    } else {
                        row.put(key, value);
                    }
                }
                data.add(row);
            }
        }

        return data;
    }
}
