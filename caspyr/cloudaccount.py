import requests
import json
import os
import sys
from abc import ABCMeta, abstractmethod, ABC


class Base(metaclass=ABCMeta):
	"""
	Abstract Base Class for all Cloud Account classes.
	"""

	def __init__(self, cloudaccount):
		self.id = cloudaccount['id']
		self.name = cloudaccount['name']
		self.enabled_region_ids = cloudaccount['enabledRegionIds']
		self.organization = cloudaccount['organizationId']
		self.self_link = cloudaccount['selfLink']
		self._links = cloudaccount['_links']
		self.custom_properties = cloudaccount['customProperties']
		try:
			self.type = cloudaccount['type']
		except KeyError:
			pass
		try:
			self.description = cloudaccount['description']
		except KeyError:
			pass

	@classmethod
	@abstractmethod
	def list(self, session, uri):
		"""
		Returns a list of account ids.
		"""
		return (session._request(uri=f'{session.baseurl}{uri}'))

	@classmethod
	@abstractmethod
	def describe(cls, session, uri):
		"""
		Returns the detail of a cloud account.
		"""
		return (session._request(uri=f'{session.baseurl}{uri}'))

	@classmethod
	@abstractmethod
	def create(cls, session, uri, data):
		"""
		Creates a Cloud Account.
		"""
		return session._request(uri=f'{session.baseurl}{uri}', request_method='POST', json=data)

	@classmethod
	@abstractmethod
	def unregister(cls, session, uri):
		"""
		Removes the cloud account from cloud assembly only, leaves it registered in discovery.
		"""
		return session._request(uri=f'{session.baseurl}{uri}', request_method='DELETE')

	@staticmethod
	@abstractmethod
	def delete(session, uri):
		"""
		Removes the cloud account from discovery, and all other services.
		"""
		return session._request(uri=f'{session.baseurl}{uri}', request_method='DELETE')


class CloudAccount(Base):
	"""
	Class for Cloud Account methods.
	"""

	def __init__(self, cloudaccount):
		super().__init__(cloudaccount)

	@classmethod
	def list(cls, session):
		uri = '/iaas/cloud-accounts'
		return super().list(session, uri)

	@classmethod
	def describe(cls, session, id):
		uri = f'/iaas/cloud-accounts/{id}'
		return cls(super().describe(session, uri))

	@classmethod
	def unregister(cls, session, id):
		uri = f'/api/cloud-accounts/{id}'
		return super().unregister(session, uri)

	@classmethod
	def delete(cls, session, id):
		uri = f'/iaas/cloud-accounts/{id}'
		return super().delete(session, uri)

	@classmethod
	def create(cls):
		pass


class CloudAccountAws(Base):
	"""
	Class for AWS Cloud Account methods.
	"""

	def __init__(self, cloudaccount):
		super().__init__()

	@classmethod
	def list(cls, session):
		uri = '/iaas/cloud-accounts-aws'
		return super().list(session, uri)

	def describe(self, session, id):
		uri = f'/iaas/cloudaccounts-aws/{id}'
		self.describe(session, uri)

	@classmethod
	def unregister(cls, session, id):
		uri = f'/api/cloud-accounts-aws/{id}'
		return super().unregister(session, uri)

	@classmethod
	def delete(cls, session, id):
		uri = f'/iaas/cloud-accounts-aws/{id}'
		return super().delete(session, uri)

	@classmethod
	def create(cls, session, name, access_key, secret_key, regions='us-west-1', create_zone=False, description=''):
		uri = '/iaas/cloud-accounts-aws'
		body = {
			"name": name,
			"description": description,
			"accessKeyId": access_key,
			"secretAccessKey": secret_key,
			"regionIds": [regions],
			"createDefaultZones": create_zone
		}
		return cls(super().create(session, uri=uri, data=body))


class CloudAccountAzure(Base):

	@classmethod
	def list(cls, session):
		uri = '/iaas/cloud-accounts-azure'
		return super().list(session, uri)

	@classmethod
	def describe(cls, session, id):
		uri = f'/iaas/cloudaccounts-azure/{id}'
		return cls(super().describe(session, uri))

	@classmethod
	def unregister(cls, session, id):
		uri = f'/api/cloud-accounts-azure/{id}'
		return super().unregister(session, uri)

	@classmethod
	def delete(cls, session, id):
		uri = f'/iaas/cloud-accounts-azure/{id}'
		return super().delete(session, uri)

	@classmethod
	def create(cls, session, name, subscription_id, tenant_id, application_id, application_key, regions='westus',
				create_zone=False, description=''):
		body = {
			"name": name,
			"description": description,
			"subscriptionId": subscription_id,
			"tenantId": tenant_id,
			"clientApplicationId": application_id,
			"clientApplicationSecretKey": application_key,
			"regionIds": [regions],
			"createDefaultZones": create_zone
		}
		uri = '/iaas/cloud-accounts-azure'
		return cls(super().create(session, uri=uri, data=body))


class CloudAccountvSphere(Base):

	@classmethod
	def list(cls, session):
		uri = '/iaas/cloud-accounts-vsphere'
		return super().list(session, uri)

	@classmethod
	def describe(cls, session, id):
		uri = f'/iaas/cloudaccounts-vsphere/{id}'
		return super().describe(session, uri)

	@classmethod
	def unregister(cls, session, id):
		uri = f'/api/cloud-accounts-vsphere/{id}'
		return super().unregister(session, uri)

	@classmethod
	def delete(cls, session, id):
		uri = f'/iaas/cloud-accounts-vsphere/{id}'
		return super().delete(session, uri)

	@classmethod
	def create(cls, session, name, fqdn, rdc, username, password, datacenter_moid, nsx_cloud_account='',
				description=''):
		uri = '/iaas/cloud-accounts-azure'
		body = {
			"name": name,
			"description": description,
			"hostName": fqdn,
			"acceptSelfSignedCertificate": True,
			"linkedCloudAccountLink": nsx_cloud_account,
			"dcid": rdc,
			"username": username,
			"password": password,
			"regionIds": datacenter_moid,
			"createDefaultZones": False
		}
		return cls(super().create(session, uri, body))


class CloudAccountNSXT(Base):

	@classmethod
	def list(cls, session):
		uri = '/iaas/cloud-accounts-nsxt'
		return super().list(session, uri)

	def describe(self, session, id):
		uri = f'/iaas/cloudaccounts-nsxt/{id}'
		self.describe(session, uri)

	@classmethod
	def unregister(cls, session, id):
		uri = f'/api/cloud-accounts-nsxt/{id}'
		return super().unregister(session, uri)

	@classmethod
	def delete(cls, session, id):
		uri = f'/iaas/cloud-accounts-nsxt/{id}'
		return super().delete(session, uri)

	@classmethod
	def createNSXT(cls, session, name, fqdn, rdc, username, password, description=''):
		uri = '/iaas/cloud-accounts-nsxt'
		body = {
			"name": name,
			"description": description,
			"hostName": fqdn,
			"acceptSelfSignedCertificate": True,
			"dcid": rdc,
			"username": username,
			"password": password,
			"createDefaultZones": False
		}
		return cls(super().create(session, uri, body))
