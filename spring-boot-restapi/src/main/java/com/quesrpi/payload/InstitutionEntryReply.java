package com.quesrpi.payload;
import org.bson.types.ObjectId;

import com.quesrpi.beans.Institution;

public class InstitutionEntryReply {

	ObjectId _id;
	String name;
	String location;
	String machine_id;
	String uploadStatus;
	
	
	public InstitutionEntryReply(Institution i,String status) {
		_id = i.get_oid();
		name=i.getName();
		location=i.getLocation();
		machine_id = i.getMachine_id();
		uploadStatus= status;
		
	}
	
	public String getId() {
		return _id.toHexString();
	}
	public void setId(ObjectId id) {
		this._id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getLocation() {
		return location;
	}
	public void setLocation(String location) {
		this.location = location;
	}
	public String getUploadStatus() {
		return uploadStatus;
	}
	public void setUploadStatus(String uploadStatus) {
		this.uploadStatus = uploadStatus;
	}

	public String getMachine_id() {
		return machine_id;
	}

	public void setMachine_id(String machine_id) {
		this.machine_id = machine_id;
	}
	
	
}
