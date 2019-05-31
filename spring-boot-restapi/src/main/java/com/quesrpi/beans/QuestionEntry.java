package com.quesrpi.beans;

import java.util.List;
import java.util.ArrayList;

//Currently doing this using a list, later will change this to a database

public class QuestionEntry {

	public List<Question> stored_data;
	
	//to store the object in the class itself (singular class)
	private static QuestionEntry qent = null;	
	
	private QuestionEntry() {
		stored_data = new ArrayList<Question>();
	}
	
	public static QuestionEntry getInstance() {
		
		if(qent == null) {
			qent = new QuestionEntry();
			return qent;
		}
		else
			return qent;
	}
	
	public int getNewId() {
		//this currently returns the index of the new entry as the id of question
		return stored_data.size();
	}
	
	public void add(Question q) {
		stored_data.add(q);
	}
	
	public List<Question> getStoredRecords(){
		return stored_data;
	}
	
	
}
