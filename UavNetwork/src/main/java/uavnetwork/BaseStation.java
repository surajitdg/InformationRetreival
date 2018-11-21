package uavnetwork;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Random;

import javax.vecmath.Point3d;
import javafx.scene.shape.Circle;

public class BaseStation
{

	private static List<Uav> uavList;

	public static void main(String args[])
	{
		int num = 3;

		uavList = new ArrayList<Uav>();

		Random r = new Random(System.currentTimeMillis());

		double x;
		double y;
		double z;

		for (int i = 0; i < num; i++)
		{
			x = r.nextInt(1000 - 0 + 1) + 0;
			y = r.nextInt(1000 - 0 + 1) + 0;
			z = r.nextInt(100 - 0 + 1) + 0;

			Point3d center = new Point3d(x, y, z);
			Uav uav = new Uav(i, center, 100, 70);

			uav.setArea(new Circle(center.x, center.y, uav.getRadius()));

			uavList.add(uav);
		}

		for (int i = 0; i < num; i++)
		{
			int j = (i+1) % num;
			Uav uav1 = uavList.get(i);
			Uav uav2 = uavList.get(j);
			List<Uav> neighbours1 = uav1.getNeighbours();
			List<Uav> neighbours2 = uav1.getNeighbours();
			
			
			neighbours1.add(uav2);
			neighbours2.add(uav1);
			
			Queue<Packet> trQ1 = new LinkedList<Packet>();
			uav1.getTranQueue().put(j, trQ1);

			Queue<Packet> reQ1 = new LinkedList<Packet>();
			uav1.getRecQueue().put(j, reQ1);
			
			Queue<Packet> trQ2 = new LinkedList<Packet>();
			uav2.getTranQueue().put(i, trQ2);

			Queue<Packet> reQ2 = new LinkedList<Packet>();
			uav2.getRecQueue().put(i, reQ2);

			NeighbourProperties nprop = new NeighbourProperties();

			double distance = UtilityFunctions.interUavDistance(uav1.getCenter(), uav2.getCenter());

			nprop.setDistance(distance);
			nprop.setBandwidth(10000000.0);
			
			
			uav1.getnProp().put(j, nprop);
			uav2.getnProp().put(i, nprop);
			

		}
		
		int counter = 0;
		
		while(counter<=180)
		{
			Packet p = UtilityFunctions.generatePacket(num);
			
			int sender = p.getSenderId();
			int receiver = p.getRecevierId();
			
			Uav uavSender = uavList.get(sender);
			Uav uavReceiver = uavList.get(receiver);
			
			if(counter%2==0)
			{
				//System.out.println("Inside BaseStation class Sender = "+ sender +"Receiver = "+receiver);
				uavSender.getTranQueue().get(receiver).add(p);
			}
			else
			{
				//System.out.println("Inside BaseStation class Sender = "+ sender +"Receiver = "+receiver);
				uavReceiver.getRecQueue().get(sender).add(p);
			}
			
			counter++;
		}

		for (Uav uav : uavList)
		{
			System.out.println("ID : "+ uav.getUavId());
			for(Map.Entry<Integer, Queue<Packet>> entry : uav.getTranQueue().entrySet())
			{
				System.out.println("Link - "+entry.getKey());
				System.out.println("TransQueue Length - "+entry.getValue().size());
			}
			for(Map.Entry<Integer, Queue<Packet>> entry : uav.getRecQueue().entrySet())
			{
				System.out.println("Link - "+entry.getKey());
				System.out.println("RecVQueue Length - "+entry.getValue().size());
			}
		}
	}
}
