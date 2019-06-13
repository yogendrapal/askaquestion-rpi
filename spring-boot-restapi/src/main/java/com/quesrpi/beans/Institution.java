package com.quesrpi.beans;
import org.bson.types.ObjectId;


public class Institution {

	public ObjectId _id;
	
	String name;
	String location;
	String machine_id;
	
	public Institution(ObjectId _id, String name, String location,String machine_id) {
		this._id = _id;
		this.name = name;
		this.location = location;
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
	public String getMachine_id() {
		return machine_id;
	}
	public void setMachine_id(String machine_id) {
		this.machine_id = machine_id;
	}
	
	
}
