package com.quesrpi.controllers;

import com.quesrpi.beans.Question;
import com.quesrpi.payload.QuestionEntryReply;
import com.quesrpi.service.QuestionRepository;

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
@RequestMapping("/question")
public class QuestionController {
	
	@Autowired
	private QuestionRepository repository;
	
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public List<Question> getAllQuestions() {
	  return repository.findAll();
	}
	
	@RequestMapping(value = "/{id}", method = RequestMethod.GET)
	public Question getQuestionById(@PathVariable("id") ObjectId id) {
	  return repository.findBy_id(id);
	  
	}
	
	@RequestMapping(value = "/{id}", method = RequestMethod.PUT)
	public void modifyQuestionById(@PathVariable("id") ObjectId id, @Valid @RequestBody Question q) {
	  q.set_id(id);
	  repository.save(q);
	}
	
	@RequestMapping(value = "/add", method = RequestMethod.POST)
	public QuestionEntryReply createQuestion(@Valid @RequestBody Question q) {
	  q.set_id(ObjectId.get());
	  repository.save(q);
	  QuestionEntryReply qrply = new QuestionEntryReply(q, "Successful");
	  return qrply;
	}
	
	@RequestMapping(value = "/{id}", method = RequestMethod.DELETE)
	public void deleteQuestion(@PathVariable ObjectId id) {
	  repository.delete(repository.findBy_id(id));
	}
	
}
