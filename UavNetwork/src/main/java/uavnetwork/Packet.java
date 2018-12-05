package uavnetwork;

public class Packet
{
	private int packetId;
	private int senderId;
	private int recevierId;
	private static final int size=50000;
	
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
	public static int getSize()
	{
		return size;
	}

	
	
}
