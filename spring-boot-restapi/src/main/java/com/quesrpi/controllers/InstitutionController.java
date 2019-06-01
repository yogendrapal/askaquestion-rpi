package com.quesrpi.controllers;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import com.quesrpi.beans.InstitutionEntry;
import com.quesrpi.beans.Institution;
import com.quesrpi.payload.InstitutionEntryReply;



@Controller

public class InstitutionController {

	@RequestMapping(method = RequestMethod.POST, value="/institution/add")
	  @ResponseBody
	  public InstitutionEntryReply newInstitution(@RequestBody Institution q) {
	  System.out.println("New Institution");
	  		InstitutionEntryReply qentreply = new InstitutionEntryReply();
	  		//q.setInstitute_id(InstitutionEntry.getInstance().getNewId());
	  		InstitutionEntry.getInstance().add(q);
	        //We are setting the below value just to reply a message back to the caller
	  		qentreply.setInstitute_id(q.getInstitute_id());
	  		qentreply.setName(q.getName());
	  		qentreply.setLocation(q.getLocation());
	        qentreply.setUploadStatus("Successful");
	        return qentreply;
	}
	
	

	@RequestMapping(method = RequestMethod.GET, value="/institution/")
	
	@ResponseBody
	  public List<Institution> getAllInsitutions() {
	  return InstitutionEntry.getInstance().getStoredRecords();
	  }
	
}
