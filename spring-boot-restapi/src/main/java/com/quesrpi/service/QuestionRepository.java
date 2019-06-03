package com.quesrpi.service;

import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Service;

import com.quesrpi.beans.Question;
@Service
public interface QuestionRepository extends MongoRepository<Question, String>{
	Question findBy_id(ObjectId _id);
	
	
}
