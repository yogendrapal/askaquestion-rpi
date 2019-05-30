package com.quesrpi.controllers;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import com.quesrpi.beans.Question;
import com.quesrpi.beans.QuestionEntry;;

@Controller
public class RetrieveController {
	
	
	@RequestMapping(method = RequestMethod.GET, value="/question/")
	
	@ResponseBody
	  public List<Question> getAllQuestions() {
	  return QuestionEntry.getInstance().getStoredRecords();
	  }
}
