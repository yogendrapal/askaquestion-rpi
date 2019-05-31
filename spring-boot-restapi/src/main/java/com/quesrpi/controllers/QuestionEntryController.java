package com.quesrpi.controllers;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import com.quesrpi.beans.*;
import com.quesrpi.payload.QuestionEntryReply;

@Controller
public class QuestionEntryController {
	@RequestMapping(method = RequestMethod.POST, value="/question/add")
	  @ResponseBody
	  public QuestionEntryReply newQuestion(@RequestBody Question q) {
	  System.out.println("In newQuestin");
	  		QuestionEntryReply qentreply = new QuestionEntryReply();
	  		q.setId(QuestionEntry.getInstance().getNewId());
	  		QuestionEntry.getInstance().add(q);
	        //We are setting the below value just to reply a message back to the caller
	  		qentreply.setId(q.getId());
	  		qentreply.setDate(q.getDate());
	  		qentreply.setTime(q.getTime());
	  		qentreply.setMachine_id(q.getMachine_id());
	        qentreply.setUploadStatus("Successful");
	        return qentreply;
	}
}
