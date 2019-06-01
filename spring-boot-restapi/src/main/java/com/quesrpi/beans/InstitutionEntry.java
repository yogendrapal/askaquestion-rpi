package com.quesrpi.beans;

import java.util.ArrayList;
import java.util.List;

public class InstitutionEntry {

public List<Institution> stored_data;
	
	//to store the object in the class itself (singular class)
	private static InstitutionEntry qent = null;	
	
	private InstitutionEntry() {
		stored_data = new ArrayList<Institution>();
	}
	
	public static InstitutionEntry getInstance() {
		
		if(qent == null) {
			qent = new InstitutionEntry();
			return qent;
		}
		else
			return qent;
	}
	
	public int getNewId() {
		//this currently returns the index of the new entry as the id of institution
		return stored_data.size();
	}
	
	public void add(Institution q) {
		stored_data.add(q);
	}
	
	public List<Institution> getStoredRecords(){
		return stored_data;
	}
	

}

