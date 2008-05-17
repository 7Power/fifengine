import fife
from serializers import *

class ObjectLocation(fife.ResourceLocation):
	def __init__(self, file, node=None):
		fife.ResourceLocation.__init__(self, file)
		self.node = node

class XMLObjectLoader(fife.ObjectLoader):
	def __init__(self, image_pool, anim_pool, model, vfs=None, dataset=None):
		self.image_pool = image_pool
		self.anim_pool = anim_pool
		self.model = model
		self.metamodel = model.getMetaModel()
		self.dataset=dataset
		self.vfs = vfs
		self.source = None
		self.filename = ''

	def loadResource(self, location):
		# store information about stuff to be loaded, after that do actual loading under @guarded
		self.source = location
		self.filename = self.source.getFilename()
		self.node = None
		if hasattr(location, 'node'):
			self.node = location.node
		self.do_load_resource()
	
	@guarded
	def do_load_resource(self):
		if self.node == None:
			f = self.vfs.open(self.source)
			tree = ET.parse(f)
			self.node = tree.getroot()
		self.parse_object(self.dataset, self.node)

	def parse_object(self, dataset, object):
		if self.node.tag != 'object':
			raise InvalidFormat('Expected <object> tag, but found <%s>.' % node.tag)
		
		id = object.get('id')
		if not id:
			raise InvalidFormat('<object> declared without an id attribute.')
		
		obj = None
		parent = object.get('parent', None)
		if parent:
			query = self.metamodel.getObjects('id', str(parent))
			if len(query) == 0:
				raise NotFound('No objects found with identifier %s.' % str(parent))
			elif len(query) > 1:
				raise NameClash('%d objects found with identifier %s.' % (len(query), str(parent)))
			parent = query[0]
		obj = dataset.createObject(str(id), parent)
		fife.ObjectVisual.create(obj)

		obj.setBlocking(bool( object.get('blocking', False) ))
		obj.setStatic(bool( object.get('static', False) ))
		
		pather = object.get('pather', 'RoutePather')
		obj.setPather( self.model.getPather(pather) )

		self.parse_images(object, obj)
		self.parse_actions(object, obj)

	def parse_images(self, objelt, object):
		for image in objelt.findall('image'):
			source = image.get('source')
			if not source:
				raise InvalidFormat('<image> declared without a source attribute.')

			id = self.image_pool.addResourceFromFile( str(source) )
			object.get2dGfxVisual().addStaticImage(int( image.get('direction', 0) ), id)
			img = self.image_pool.getImage(id)
			img.setXShift(int( image.get('x_offset', 0) ))
			img.setYShift(int( image.get('y_offset', 0) ))

	def parse_actions(self, objelt, object):
		for action in objelt.findall('action'):
			id = action.get('id')
			if not id:
				raise InvalidFormat('<action> declared without an id attribute.')
	
			act_obj = object.createAction(str(id))
			fife.ActionVisual.create(act_obj)
			self.parse_animations(action, act_obj)

	def parse_animations(self, actelt, action):
		for anim in actelt.findall('animation'):
			source = anim.get('source')
			if not source:
				raise InvalidFormat('Animation declared with no source location.')
			
			anim_id = self.anim_pool.addResourceFromFile(str(source))
			animation = self.anim_pool.getAnimation(anim_id)
			action.get2dGfxVisual().addAnimation(int( anim.get('direction', 0) ), anim_id)
			action.setDuration(animation.getDuration())
