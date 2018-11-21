package uavnetwork;

public class Packet
{
	private int packetId;
	private int senderId;
	private int recevierId;
	private int size;
	
	public int getPacketId()
	{
		return packetId;
	}
	public void setPacketId(int packetId)
	{
		this.packetId = packetId;
	}
	public int getSenderId()
	{
		return senderId;
	}
	public void setSenderId(int senderId)
	{
		this.senderId = senderId;
	}
	public int getRecevierId()
	{
		return recevierId;
	}
	public void setRecevierId(int recevierId)
	{
		this.recevierId = recevierId;
	}
	public int getSize()
	{
		return size;
	}
	public void setSize(int size)
	{
		this.size = size;
	}
	
	
}
