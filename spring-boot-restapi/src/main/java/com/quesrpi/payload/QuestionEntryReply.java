package com.quesrpi.payload;

import org.bson.types.ObjectId;

import com.quesrpi.beans.Question;

public class QuestionEntryReply {
	ObjectId _id;
	String date;
	String time;
	String machine_id;
	String uploadStatus;
	
	public QuestionEntryReply(Question q, String status) {
		_id = q.get_oid();
		date = q.getDate();
		time = q.getTime();
		machine_id = q.getMachine_id();
		uploadStatus = status;
	}
	
	public String getId() {
		return _id.toHexString();
	}
	public void setId(ObjectId id) {
		this._id = id;
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
	public String getUploadStatus() {
		return uploadStatus;
	}
	public void setUploadStatus(String uploadStatus) {
		this.uploadStatus = uploadStatus;
	}
	
	
	
}
