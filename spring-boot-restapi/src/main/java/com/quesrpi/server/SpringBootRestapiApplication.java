package com.quesrpi.server;

import com.quesrpi.property.FileStorageProperties;
import com.quesrpi.service.QuestionRepository;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@EnableConfigurationProperties({
    FileStorageProperties.class
})
@SpringBootApplication(scanBasePackages = {"com.quesrpi","com.quesrpi.service"})
@EnableMongoRepositories(basePackageClasses = QuestionRepository.class)
public class SpringBootRestapiApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringBootRestapiApplication.class, args);
	}

}
