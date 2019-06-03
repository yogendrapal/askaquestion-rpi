package com.quesrpi.controllers;

import com.quesrpi.beans.Institution;
import com.quesrpi.payload.InstitutionEntryReply;
import com.quesrpi.service.InstitutionRepository;

import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/institution")
public class InstitutionController {
	
	@Autowired
	private InstitutionRepository repository;
	
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public List<Institution> getAllInstitutions() {
	  return repository.findAll();
	}
	
	@RequestMapping(value = "/{id}", method = RequestMethod.GET)
	public Institution getInstitutionById(@PathVariable("id") ObjectId id) {
	  return repository.findBy_id(id);
	}
	
	@RequestMapping(value = "/{id}", method = RequestMethod.PUT)
	public void modifyInstitutionById(@PathVariable("id") ObjectId id, @Valid @RequestBody Institution i) {
	  i.set_id(id);
	  repository.save(i);
	}
	
	@RequestMapping(value = "/add", method = RequestMethod.POST)
	public InstitutionEntryReply createInstitution(@Valid @RequestBody Institution i) {
	  i.set_id(ObjectId.get());
	  repository.save(i);
	  InstitutionEntryReply irply = new InstitutionEntryReply(i, "Successful");
	  return irply;
	}
	
	@RequestMapping(value = "/{id}", method = RequestMethod.DELETE)
	public void deleteInstitution(@PathVariable ObjectId id) {
	  repository.delete(repository.findBy_id(id));
	}
	
}
