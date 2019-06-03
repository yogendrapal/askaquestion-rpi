package com.quesrpi.repositories;

import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.repository.MongoRepository;

import com.quesrpi.beans.Question;

public interface QuestionRepository extends MongoRepository<Question, String>{
	Question findBy_id(ObjectId _id);
}
