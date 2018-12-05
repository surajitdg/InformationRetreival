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

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javafx.scene.shape.Circle;

public class BaseStation
{

	private static List<Uav> uavList;
	private static Properties prop;
	private static int transDropCount = 0;
	private static int recvDropCount = 0;
	private static final Logger logger = LoggerFactory.getLogger(BaseStation.class);

	public static void generatePackets(int num, boolean flag)
	{
		int counter = 0;
		Random r = new Random(System.currentTimeMillis());
		int limit;

		// limit = r.nextInt(250);

		limit = r.nextInt(500) + 150;
		while (counter <= limit)

		{
			Packet pkt = UtilityFunctions.generatePacket(num);

			int senderId = pkt.getSenderId();
			int receiverId = pkt.getRecevierId();
			// logger.info("Sender = " + sender + " Receiver = " + receiver);
			Uav uavSender = uavList.get(senderId);
			int viaNode = uavSender.getRoutingTable().get(receiverId);
			// logger.info("Via Node =" + viaNode);
			// Uav uavReceiver = uavList.get(receiver);

			if (uavSender.getTranQueue().get(viaNode).size() < 400)
				uavSender.getTranQueue().get(viaNode).add(pkt);
			else
			{
				transDropCount++;
				logger.info("Packet ID : " + pkt.getPacketId() + " from sender " + senderId + " to receiver "

						+ receiverId + " has been dropped and couldn't be added to transmission queue of "
						+ uavSender.getUavId() + " as the size is full ; Size "
						+ uavSender.getTranQueue().get(viaNode).size());
			}

			/*
			 * if(flag) { if (counter % 2 == 0) { //
			 * logger.info("Inside BaseStation class Sender = "+ sender +"Receiver = //
			 * "+receiver);
			 * 
			 * } else { // logger.info("Inside BaseStation class Sender = "+ sender
			 * +"Receiver = // "+receiver); uavReceiver.getRecQueue().get(sender).add(p); }
			 * } else {
			 * 
			 * }
			 */

			counter++;
		}

	}

	public static void transmitPackets(Uav uav, boolean lessThanThreshold)
	{
		int time = 60;

		/*
		 * if (lessThanThreshold) time = 60; else time = 58;
		 */

		String[] nbr = prop.getProperty("" + uav.getUavId()).split(",");
		for (int p = 0; p < nbr.length; p++)
		{
			int nbrId = Integer.parseInt(nbr[p]);
			double distance = uav.getnProp().get(nbrId).getDistance();
			double bandwidth = uav.getnProp().get(nbrId).getBandwidth();
			double length = (bandwidth * distance) / (2000000);
			int factor = time * (int) distance / 2000000;
			int numOfPackets = (int) length / Packet.getSize();
			numOfPackets *= factor;
			while (numOfPackets >= 0 && uav.getTranQueue().get(nbrId).size() >= 1)
			{
				Packet pkt = uav.getTranQueue().get(nbrId).poll();
				int senderId = pkt.getSenderId();
				int receiverId = pkt.getRecevierId();
				// Uav recUav = uavList.get(receiverId);
				Uav recUav = uavList.get(nbrId);
				if (recUav.getRecQueue().get(uav.getUavId()).size() < 400)
				{
					recUav.getRecQueue().get(uav.getUavId()).add(pkt);

					logger.info("Packet ID : " + pkt.getPacketId() + " from sender " + senderId + " to receiver "
							+ receiverId + " removed from transmission queue of " + uav.getUavId()
							+ " and added to receiving queue of " + recUav.getUavId());
				} else
				{
					recvDropCount++;
					logger.info("Packet ID : " + pkt.getPacketId() + " from sender " + senderId + " to receiver "
							+ receiverId + " has been dropped and couldn't be added to receiving queue of "
							+ recUav.getUavId() + " as the size is full ; Size "
							+ recUav.getRecQueue().get(uav.getUavId()).size());
				}
			}
		}
	}

	public static void deliverPackets(Uav uav)
	{

		String[] nbr = prop.getProperty("" + uav.getUavId()).split(",");
		for (int p = 0; p < nbr.length; p++)
		{
			int nbrId = Integer.parseInt(nbr[p]);
			int k = 1000;
			logger.info("Size of queue before delivering " + uav.getRecQueue().get(nbrId).size());
			while (k >= 1 && uav.getRecQueue().get(nbrId).size() >= 1)
			{
				Packet pkt = uav.getRecQueue().get(nbrId).poll();
				// logger.info("Packet delivered from the queue "+nbrId+ " of the uav
				// "+uav.getUavId());
				if (pkt.getRecevierId() != uav.getUavId())
				{
					int viaNode = uav.getRoutingTable().get(pkt.getRecevierId());
					uav.getTranQueue().get(viaNode).add(pkt);
				} else
				{
					logger.info("Packet ID : " + pkt.getPacketId() + " from sender " + pkt.getSenderId()
							+ " to receiver " + pkt.getRecevierId() + " removed from receiving queue of "
							+ uav.getUavId() + " and delivered");
				}
				k--;
			}
			logger.info("Size of queue after delivering " + uav.getRecQueue().get(nbrId).size());
		}
	}

	public static void main(String args[]) throws IOException
	{
		int num = 9;

		uavList = new ArrayList<Uav>();
		prop = new Properties();
		InputStream is = new FileInputStream("src/main/resources/config.ini");
		prop.load(is);

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
			logger.info("ID = " + i);
			for (int p = 0; p < nbr.length; p++)
			{
				int j = Integer.parseInt(nbr[p]);
				logger.info("Neighbour = " + j);
				Uav uav1 = uavList.get(i);
				Uav uav2 = uavList.get(j);
				List<Uav> neighbours1 = uav1.getNeighbours();
				List<Uav> neighbours2 = uav2.getNeighbours();

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

			for (int j = 0; j < num; j++)
			{
				if (i != j)
				{
					int viaNode = Integer.parseInt(prop.getProperty(i + "" + j));
					uavList.get(i).getRoutingTable().put(j, viaNode);
				}

			}

		}

		int counter = 0;
		int count = 0;
		while (count <= 60)
		{
			logger.info("********************************************Iteration number " + count
					+ " ********************************************");

			if (count == 0)
			{
				generatePackets(num, true);
			}

			else
			{
				for (Uav uav : uavList)
				{

					// Write code to transmit from transmission queue
					// logger.info("id : "+ );

					boolean lessThanThreshold = true;
					int movId = -1;
					String[] nbr = prop.getProperty("" + uav.getUavId()).split(",");
					for (int p = 0; p < nbr.length; p++)
					{
						int nbrId = Integer.parseInt(nbr[p]);
						int size = uav.getTranQueue().get(nbrId).size();
						if (size > 75)
						{
							lessThanThreshold = false;
							movId = nbrId;
							break;
						}
					}

					if (!lessThanThreshold)
					{
						double x_coord = Double.parseDouble(prop.getProperty("center_" + uav.getUavId()).split(",")[0]);
						double y_coord = Double.parseDouble(prop.getProperty("center_" + uav.getUavId()).split(",")[1]);
						Point3d p = UtilityFunctions.movement(uav.getCenter(), uavList.get(movId).getCenter(), 5.0,
								x_coord, y_coord);
						uav.setCenter(p);
						uav.setPositionChanged(true);

						for (Uav uav2 : uav.getNeighbours())
						{
							double distance = UtilityFunctions.interUavDistance(uav.getCenter(), uav2.getCenter());
							uav.getnProp().get(uav2.getUavId()).setDistance(distance);
							uav2.getnProp().get(uav.getUavId()).setDistance(distance);
						}
					}

					if (uav.isPositionChanged() && lessThanThreshold)
					{
						double x_coord = Double.parseDouble(prop.getProperty("center_" + uav.getUavId()).split(",")[0]);
						double y_coord = Double.parseDouble(prop.getProperty("center_" + uav.getUavId()).split(",")[1]);
						uav.setCenter(new Point3d(x_coord, y_coord, 30));

						for (Uav uav2 : uav.getNeighbours())
						{
							double distance = UtilityFunctions.interUavDistance(uav.getCenter(), uav2.getCenter());
							uav.getnProp().get(uav2.getUavId()).setDistance(distance);
							uav2.getnProp().get(uav.getUavId()).setDistance(distance);
						}
					}
					logger.info(
							"-------------------------------------------------------------------------------------------------------------------------------------");
					transmitPackets(uav, lessThanThreshold);
					logger.info(
							"-------------------------------------------------------------------------------------------------------------------------------------");
					generatePackets(num, false);
				}
			}

			for (Uav uav : uavList)
			{

				logger.info("ID : " + uav.getUavId() + " co-ordinates : (" + uav.getCenter().x + ", "
						+ uav.getCenter().y + ", " + uav.getCenter().z + ")");
				for (Map.Entry<Integer, Queue<Packet>> entry : uav.getTranQueue().entrySet())
				{
					logger.info("Link - " + entry.getKey());
					logger.info("TransQueue Length - " + entry.getValue().size());
				}
				for (Map.Entry<Integer, Queue<Packet>> entry : uav.getRecQueue().entrySet())
				{
					logger.info("Link - " + entry.getKey());
					logger.info("RecVQueue Length - " + entry.getValue().size());
				}
				logger.info(
						"-------------------------------------------------------------------------------------------------------------------------------------");

				deliverPackets(uav);
				logger.info(
						"-------------------------------------------------------------------------------------------------------------------------------------");
			}
			count++;
		}
		logger.info("Total number of packets generated in simulation time = " + UtilityFunctions.getCount());
		logger.info("Packets dropped because transmission queue full = " + transDropCount);
		logger.info("Packets dropped because receiving queue full = " + recvDropCount);

	}
}
