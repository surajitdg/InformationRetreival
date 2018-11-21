package uavnetwork;

import java.util.Random;

import javax.vecmath.Point3d;

public class UtilityFunctions
{
	public static double interUavDistance(Point3d p1, Point3d p2)
	{
		double distance = p1.distance(p2);
		return distance;
	}
	
	public static Packet generatePacket(int num)
	{
		Packet p = new Packet();
		
		Random r = new Random();
		int sender = r.nextInt(num);
		int receiver = r.nextInt(num);
		
		if(sender == receiver)
			{
				//System.out.println("Sender = "+ sender +"Receiver = "+receiver);
				receiver = (sender+1)%num;
				//System.out.println("Sender = "+ sender +"Receiver = "+receiver);
			}
		
		p.setPacketId(r.nextInt());
		p.setSenderId(sender);
		p.setRecevierId(receiver);
			
		
		return p;
	}
	
	public static void main(String ar[])
	{
		Point3d p1 = new Point3d(3.0, 4.0, 5.0);
		Point3d p2 = new Point3d(3.0, 4.0, 7.0);
		
		System.out.println(interUavDistance(p1, p2));
	}
}
