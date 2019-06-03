package com.quesrpi.beans;

import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;

public class Question {
	
	//this id is the _id of the mongodb object
	@Id
	public ObjectId _id;
	
	String date;
	String time;
	String machine_id;
	
	public Question() {
		
	}
	
	public Question(ObjectId _id, String date, String time, String machine_id) {
		this._id = _id;
		this.date = date;
		this.time = time;
		this.machine_id = machine_id;
	}
	// ObjectId is converted to Hex string
	public String get_id() {
		return _id.toHexString();
	}
	public ObjectId get_oid() {
		return _id;
	}
	public void set_id(ObjectId _id) {
		this._id = _id;
	}
	public String getDate() {
		return date;
	}
	public void setDate(String date) {
		this.date = date;
	}
	public String getTime() {
		return time;
	}
	public void setTime(String time) {
		this.time = time;
	}
	public String getMachine_id() {
		return machine_id;
	}
	public void setMachine_id(String machine_id) {
		this.machine_id = machine_id;
	}
	
	
	
	
}
