package com.quesrpi.controllers;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StatusController {
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String getRunningStatus() {
	  return "[INFO]: Server is Running.";
	}
}
