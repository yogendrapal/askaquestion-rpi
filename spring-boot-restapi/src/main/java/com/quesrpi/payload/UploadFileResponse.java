package com.quesrpi.payload;

public class UploadFileResponse {
    private String fileName;
    private String fileDownloadUri;
    private String fileType;
    private String md5;
    private long size;
    private String status;

    public UploadFileResponse(String fileName, String fileDownloadUri, String fileType, String md5, long size) {
        this.fileName = fileName;
        this.fileDownloadUri = fileDownloadUri;
        this.fileType = fileType;
        this.md5 = md5;
        this.size = size;
        this.status = "Successful";
    }
    
    public UploadFileResponse(int code) {
    	if(code == -1) {
    		status = "No matching Question Id found";
    	}
    	this.fileName = "Error";
        this.fileDownloadUri = "Error";
        this.fileType = "Error";
        this.md5 = "Error";
        this.size = -1;
    }

	public String getStatus() {
		return status;
	}

	public void setStatus(String status) {
		this.status = status;
	}

	public String getMd5() {
		return md5;
	}

	public void setMd5(String md5) {
		this.md5 = md5;
	}

	public String getFileName() {
		return fileName;
	}

	public void setFileName(String fileName) {
		this.fileName = fileName;
	}

	public String getFileDownloadUri() {
		return fileDownloadUri;
	}

	public void setFileDownloadUri(String fileDownloadUri) {
		this.fileDownloadUri = fileDownloadUri;
	}

	public String getFileType() {
		return fileType;
	}

	public void setFileType(String fileType) {
		this.fileType = fileType;
	}

	public long getSize() {
		return size;
	}

	public void setSize(long size) {
		this.size = size;
	}

	
}