package com.quesrpi.server;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = {"com.quesrpi"})
public class SpringBootRestapiApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringBootRestapiApplication.class, args);
	}

}
