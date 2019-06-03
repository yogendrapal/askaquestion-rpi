package com.quesrpi.service;

import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Service;

import com.quesrpi.beans.Institution;
@Service
public interface InstitutionRepository extends MongoRepository<Institution, String>{
	Institution findBy_id(ObjectId _id);
	
	
}
