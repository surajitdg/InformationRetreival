package uavnetwork;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Queue;
import java.util.Random;

import javax.vecmath.Point3d;
import javafx.scene.shape.Circle;

public class BaseStation
{

	private static List<Uav> uavList;
	private static Properties prop;
	
	public static void generatePackets(int num)
	{
		int counter = 0;
		while (counter <= 1080)

		{
			Packet p = UtilityFunctions.generatePacket(num);

			int sender = p.getSenderId();
			int receiver = p.getRecevierId();

			Uav uavSender = uavList.get(sender);
			Uav uavReceiver = uavList.get(receiver);

			if (counter % 2 == 0)
			{
				// System.out.println("Inside BaseStation class Sender = "+ sender +"Receiver =
				// "+receiver);
				uavSender.getTranQueue().get(receiver).add(p);
			} else
			{
				// System.out.println("Inside BaseStation class Sender = "+ sender +"Receiver =
				// "+receiver);
				uavReceiver.getRecQueue().get(sender).add(p);
			}

			counter++;
		}

	}
	
	public static void transmitPackets(Uav uav, boolean lessThanThreshold)
	{
		int time;
		
		if(lessThanThreshold)
			time = 60;
		else
			time = 58;
		
		String[] nbr = prop.getProperty("" + uav.getUavId()).split(",");
		for(int p = 0; p<nbr.length;p++)
		{
			int nbrId = Integer.parseInt(nbr[p]);
			double distance = uav.getnProp().get(nbrId).getDistance();
			double bandwidth = uav.getnProp().get(nbrId).getBandwidth();
			double length = (bandwidth*distance)/(2000000);
			int factor = time*(int)distance/2000000;
			int numOfPackets = (int)length/10;
			numOfPackets *= factor;
			while(numOfPackets>=0 && uav.getTranQueue().get(nbrId).size()>=1)
			{
				Packet pkt = uav.getTranQueue().get(nbrId).poll();
				int senderId = pkt.getSenderId();
				int receiverId = pkt.getRecevierId();
				Uav recUav = uavList.get(receiverId);
				recUav.getRecQueue().get(senderId).add(pkt);
			}
		}
	}

	public static void main(String args[]) throws IOException
	{
		int num = 9;

		uavList = new ArrayList<Uav>();
		prop = new Properties();
		InputStream is = new FileInputStream("src/main/resources/config.ini");
		prop.load(is);
		Random r = new Random(System.currentTimeMillis());

		double x;
		double y;
		double z;

		for (int i = 0; i < num; i++)
		{

			x = Double.parseDouble(prop.getProperty("center_" + i).split(",")[0]);
			y = Double.parseDouble(prop.getProperty("center_" + i).split(",")[1]);
			z = 30.0;

			Point3d center = new Point3d(x, y, z);
			Uav uav = new Uav(i, center, 100, 70);

			uav.setArea(new Circle(center.x, center.y, uav.getRadius()));

			uavList.add(uav);
		}

		for (int i = 0; i < num; i++)
		{
			String[] nbr = prop.getProperty("" + i).split(",");

			for (int p = 0; p < nbr.length; p++)
			{
				int j = Integer.parseInt(nbr[p]);
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
				nprop.setBandwidth(1000000.0);

				uav1.getnProp().put(j, nprop);
				uav2.getnProp().put(i, nprop);

			}
		}

		int counter = 0;
		int count = 0;
		while (count <= 60)
		{
			if (count == 0)
			{
					generatePackets(num);
			}
			
			else
			{
				for(Uav uav : uavList)
				{
					
					//Write code to transmit from transmission queue
					
					
					
					boolean lessThanThreshold = true;
					int movId = -1;
					String[] nbr = prop.getProperty("" + uav.getUavId()).split(",");
					for(int p = 0; p<nbr.length;p++)
					{
						int nbrId = Integer.parseInt(nbr[p]);
						int size = uav.getTranQueue().get(nbrId).size();
						if(size > 75)
							{
								lessThanThreshold = false;
								movId = nbrId;
								break;
							}
					}
					
					if(!lessThanThreshold)
					{
						UtilityFunctions.movement(uav.getCenter(), uavList.get(movId).getCenter(), 20.0);
					}
						
					if(uav.isPositionChanged() && lessThanThreshold)
					{
						double x_coord = Double.parseDouble(prop.getProperty("center_" + uav.getUavId()).split(",")[0]);
						double y_coord = Double.parseDouble(prop.getProperty("center_" + uav.getUavId()).split(",")[1]);
						uav.setCenter(new Point3d(x_coord, y_coord, 30));
					}
					transmitPackets(uav, lessThanThreshold);
				}
			}
			System.out.println("********************************************Iteration number********************************************" + count);
			for (Uav uav : uavList)
			{
				
				System.out.println("ID : " + uav.getUavId());
				for (Map.Entry<Integer, Queue<Packet>> entry : uav.getTranQueue().entrySet())
				{
					System.out.println("Link - " + entry.getKey());
					System.out.println("TransQueue Length - " + entry.getValue().size());
				}
				for (Map.Entry<Integer, Queue<Packet>> entry : uav.getRecQueue().entrySet())
				{
					System.out.println("Link - " + entry.getKey());
					System.out.println("RecVQueue Length - " + entry.getValue().size());
				}
			}
			count++;
		}

	}
}
